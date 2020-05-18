let http = require("http");
let fs = require("fs");
let path = require("path");

let mimeTypes = {
	".html" : "text/html",
	".js" : "text/javascript",
	".css" : "text/css",
	".zip" : "application/zip"
};
// путь до папки, где хранится БД
let database = "./database"
// путь до архивированной БД
let localDatabasePath = "./database_storage/database.zip"
// последняя посещенная директория
let last_dir = "";

function main(req, res){
	console.log("Request to url ", req.url);
	// получаем имя файла
	let file_name = path.basename(req.url);
	// и его расширение
	let file_ext = String(path.extname(file_name)).toLowerCase();
	
	let file_path = "";
	let contentType = mimeTypes[file_ext];
	// если адрес пуст, то выдаем index.html
	if (file_ext.length == 0){
		file_path = "index.html";
		contentType = mimeTypes[".html"];
	}else if(file_ext == ".html"){
		// читаем список папок грабберов
		let jsonData = fs.readFileSync(database + "/index.json")
		let data = JSON.parse(jsonData);
		let grab_names = [];
		// получаем имена грабберов
		for(let name in data){
			grab_names.push(name);
		}
		// ищем нужную страницу в папках грабберов
		for(let i=0; i<grab_names.length; i++){
			let dir_path = database + '/' + grab_names[i] + "/pages";
			list = fs.readdirSync(dir_path);
			console.log(list);
			if(list.indexOf(file_name) >= 0){
				file_path = dir_path+"/"+file_name;
				last_dir = database + '/' + grab_names[i];
				break;
			}
		}
		console.log(file_path);
	}else if(file_ext == ".zip"){
		// отсылаем архив
		if(fs.existsSync(localDatabasePath))
			file_path = localDatabasePath;
		else{
			file_path = "no_local_database.html";
			contentType = mimeTypes[".html"];
		}
	}else{
		file_path = last_dir + "/style/" + file_name;
	}
	fs.readFile(file_path, (error, content) => {
		if(error){
			res.writeHead(404);
			res.end("404 not found", "utf-8");
		}else{
			if(file_path == "no_local_database.html"){
				res.writeHead(404, {"Content-Type": contentType});
				res.end(content, "utf-8");
			}else{
				res.writeHead(200, {"Content-Type": contentType});
				res.end(content, "utf-8");
			}
			
		}
	});
	
}

let port = "8080";
let server = http.createServer((req, res)=>main(req, res));
server.listen(port);
console.log("Server running at 127.0.0.1:8080");