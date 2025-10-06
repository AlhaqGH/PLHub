import '../src/runtime.dart';

Future<void> main() async {
  PohRuntime.writeFile("temp_demo.txt", "Hello", append: false);
  PohRuntime.writeFile("temp_demo.txt", " World", append: true);
  var fileContent = PohRuntime.readFile("temp_demo.txt");
  print(fileContent);
  var fileList = PohRuntime.listFiles(".");
  print(fileList);
  PohRuntime.createDirectory("backup_demo");
  PohRuntime.changeDirectory("backup_demo");
  await PohRuntime.runProgramWait("echo Hello from PohLang");
  PohRuntime.changeDirectory("..");
  PohRuntime.deleteFile("temp_demo.txt");
  PohRuntime.deleteDirectory("backup_demo");
}
