"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.createProject = void 0;
const vscode = __importStar(require("vscode"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
async function createProject() {
    try {
        // Get the workspace folder or ask user to select a directory
        let workspaceFolder;
        if (vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders.length > 0) {
            workspaceFolder = vscode.workspace.workspaceFolders[0].uri.fsPath;
        }
        else {
            const selectedFolder = await vscode.window.showOpenDialog({
                canSelectFiles: false,
                canSelectFolders: true,
                canSelectMany: false,
                openLabel: 'Select Project Directory'
            });
            if (!selectedFolder || selectedFolder.length === 0) {
                return;
            }
            workspaceFolder = selectedFolder[0].fsPath;
        }
        // Ask for project name
        const projectName = await vscode.window.showInputBox({
            prompt: 'Enter the name for your PohLang project',
            value: 'my-pohlang-project',
            validateInput: (value) => {
                if (!value || value.trim().length === 0) {
                    return 'Project name cannot be empty';
                }
                if (!/^[a-zA-Z0-9_-]+$/.test(value)) {
                    return 'Project name can only contain letters, numbers, hyphens, and underscores';
                }
                return null;
            }
        });
        if (!projectName) {
            return;
        }
        const projectPath = path.join(workspaceFolder, projectName);
        // Check if directory already exists
        if (fs.existsSync(projectPath)) {
            const overwrite = await vscode.window.showWarningMessage(`Directory "${projectName}" already exists. Do you want to continue?`, 'Yes', 'No');
            if (overwrite !== 'Yes') {
                return;
            }
        }
        // Create project directory
        if (!fs.existsSync(projectPath)) {
            fs.mkdirSync(projectPath, { recursive: true });
        }
        // Create project structure
        const srcPath = path.join(projectPath, 'src');
        if (!fs.existsSync(srcPath)) {
            fs.mkdirSync(srcPath);
        }
        // Create main.poh file
        const mainFilePath = path.join(srcPath, 'main.poh');
        const mainFileContent = `# Welcome to your new PohLang project!
# This is the main entry point for your application.
# PohLang v0.5.2 - Rust Runtime

Start Program
    Write "Hello, PohLang World!"
    Write "Welcome to your new project: ${projectName}"
    
    # Your code goes here
    Make message = "PohLang is awesome!"
    Write message
    
    # Example: Using phrasal expressions
    Make numbers = [1, 2, 3, 4, 5]
    Make sum = total of numbers
    Write "The sum is: "
    Write sum
End Program`;
        fs.writeFileSync(mainFilePath, mainFileContent);
        // Create README.md
        const readmePath = path.join(projectPath, 'README.md');
        const readmeContent = `# ${projectName}

A PohLang project created with PL-Hub.

## Getting Started

1. Open \`src/main.poh\` to start coding
2. Use Ctrl+F5 to run your PohLang files
3. Check the PohLang documentation for language syntax

## Project Structure

- \`src/\` - Source code directory
- \`src/main.poh\` - Main entry point

## Commands

- **PL-Hub: Run File** - Execute the current .poh file
- **PL-Hub: Create Project** - Create a new PohLang project
- **PL-Hub: Update Language** - Update the PohLang interpreter

Happy coding with PohLang!
`;
        fs.writeFileSync(readmePath, readmeContent);
        // Open the project in VS Code
        const projectUri = vscode.Uri.file(projectPath);
        await vscode.commands.executeCommand('vscode.openFolder', projectUri, false);
        vscode.window.showInformationMessage(`PohLang project "${projectName}" created successfully!`);
    }
    catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        vscode.window.showErrorMessage(`Error creating PohLang project: ${errorMessage}`);
    }
}
exports.createProject = createProject;
//# sourceMappingURL=createProject.js.map