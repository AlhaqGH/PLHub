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
exports.parsePohLangError = exports.PohLangError = exports.sanitizeOutput = exports.isValidPohLangFile = exports.formatError = exports.getPohLangInterpreterPath = exports.spawnPohLangProcess = void 0;
const cp = __importStar(require("child_process"));
const path = __importStar(require("path"));
const vscode = __importStar(require("vscode"));
const fs = __importStar(require("fs"));
async function spawnPohLangProcess(filePath, args = []) {
    return new Promise((resolve) => {
        try {
            // Get the interpreter path
            const interpreterPath = getPohLangInterpreterPath();
            if (!interpreterPath) {
                resolve({
                    success: false,
                    stdout: '',
                    stderr: 'PohLang interpreter not found. Please update the language using "PL-Hub: Update Language" command.',
                    exitCode: -1
                });
                return;
            }
            // Prepare command arguments with --run flag for Rust runtime v0.5.2
            const allArgs = ['--run', filePath, ...args];
            // Spawn the process
            const child = cp.spawn(interpreterPath, allArgs, {
                cwd: path.dirname(filePath),
                env: process.env
            });
            let stdout = '';
            let stderr = '';
            // Collect stdout
            child.stdout?.on('data', (data) => {
                stdout += data.toString();
            });
            // Collect stderr
            child.stderr?.on('data', (data) => {
                stderr += data.toString();
            });
            // Handle process completion
            child.on('close', (code) => {
                resolve({
                    success: code === 0,
                    stdout: stdout.trim(),
                    stderr: stderr.trim(),
                    exitCode: code
                });
            });
            // Handle process errors
            child.on('error', (error) => {
                resolve({
                    success: false,
                    stdout: '',
                    stderr: `Failed to start PohLang interpreter: ${error.message}`,
                    exitCode: -1
                });
            });
            // Set a timeout to prevent hanging
            setTimeout(() => {
                if (!child.killed) {
                    child.kill();
                    resolve({
                        success: false,
                        stdout: stdout.trim(),
                        stderr: 'Process timed out after 30 seconds',
                        exitCode: -1
                    });
                }
            }, 30000); // 30 second timeout
        }
        catch (error) {
            const errorMessage = error instanceof Error ? error.message : String(error);
            resolve({
                success: false,
                stdout: '',
                stderr: `Error executing PohLang interpreter: ${errorMessage}`,
                exitCode: -1
            });
        }
    });
}
exports.spawnPohLangProcess = spawnPohLangProcess;
function getPohLangInterpreterPath() {
    try {
        // Check multiple locations for pohlang.exe (Rust runtime v0.5.2)
        // 1. Extension's bin/ directory (bundled with extension)
        const extension = vscode.extensions.getExtension('pohlang.PLHub');
        if (extension) {
            const extensionPath = extension.extensionPath;
            const binDir = path.join(extensionPath, 'bin');
            const candidates = ['pohlang.exe', 'pohlang'];
            for (const c of candidates) {
                const full = path.join(binDir, c);
                if (fs.existsSync(full)) {
                    console.log(`Found PohLang runtime at: ${full}`);
                    return full;
                }
            }
        }
        // 2. Workspace's bin/ directory (portable distribution)
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (workspaceFolders && workspaceFolders.length > 0) {
            for (const folder of workspaceFolders) {
                const binDir = path.join(folder.uri.fsPath, 'bin');
                if (fs.existsSync(binDir)) {
                    const candidates = ['pohlang.exe', 'pohlang'];
                    for (const c of candidates) {
                        const full = path.join(binDir, c);
                        if (fs.existsSync(full)) {
                            console.log(`Found PohLang runtime at: ${full}`);
                            return full;
                        }
                    }
                }
            }
        }
        // 3. Check PohLang/runtime/target/release (development environment)
        if (workspaceFolders && workspaceFolders.length > 0) {
            for (const folder of workspaceFolders) {
                const runtimePath = path.join(folder.uri.fsPath, 'PohLang', 'runtime', 'target', 'release', 'pohlang.exe');
                if (fs.existsSync(runtimePath)) {
                    console.log(`Found PohLang runtime at: ${runtimePath}`);
                    return runtimePath;
                }
                // Also try without PohLang subdirectory
                const altRuntimePath = path.join(folder.uri.fsPath, 'runtime', 'target', 'release', 'pohlang.exe');
                if (fs.existsSync(altRuntimePath)) {
                    console.log(`Found PohLang runtime at: ${altRuntimePath}`);
                    return altRuntimePath;
                }
            }
        }
        // 4. Check environment PATH
        const pathEnv = process.env.PATH || '';
        const pathDirs = pathEnv.split(path.delimiter);
        for (const dir of pathDirs) {
            const candidates = ['pohlang.exe', 'pohlang'];
            for (const c of candidates) {
                const full = path.join(dir, c);
                if (fs.existsSync(full)) {
                    console.log(`Found PohLang runtime at: ${full}`);
                    return full;
                }
            }
        }
        console.error('PohLang runtime not found in any expected location');
        return null;
    }
    catch (error) {
        console.error('Error getting PohLang interpreter path:', error);
        return null;
    }
}
exports.getPohLangInterpreterPath = getPohLangInterpreterPath;
function formatError(error) {
    if (error instanceof Error) {
        return error.message;
    }
    else if (typeof error === 'string') {
        return error;
    }
    else {
        return 'Unknown error occurred';
    }
}
exports.formatError = formatError;
function isValidPohLangFile(filePath) {
    return filePath.endsWith('.poh');
}
exports.isValidPohLangFile = isValidPohLangFile;
function sanitizeOutput(output) {
    // Remove ANSI escape codes and control characters
    return output.replace(/\x1b\[[0-9;]*m/g, '').replace(/\r\n/g, '\n');
}
exports.sanitizeOutput = sanitizeOutput;
class PohLangError extends Error {
    constructor(message, line, column, severity = 'error') {
        super(message);
        this.line = line;
        this.column = column;
        this.severity = severity;
        this.name = 'PohLangError';
    }
}
exports.PohLangError = PohLangError;
function parsePohLangError(errorOutput) {
    const errors = [];
    const lines = errorOutput.split('\n');
    for (const line of lines) {
        // Parse different error formats
        // Format 1: "Line X: Error message"
        let match = line.match(/Line (\d+):\s*(.+)/);
        if (match) {
            const lineNumber = parseInt(match[1]);
            const message = match[2];
            errors.push(new PohLangError(message, lineNumber));
            continue;
        }
        // Format 2: "Error at line X, column Y: message"
        match = line.match(/Error at line (\d+), column (\d+):\s*(.+)/);
        if (match) {
            const lineNumber = parseInt(match[1]);
            const columnNumber = parseInt(match[2]);
            const message = match[3];
            errors.push(new PohLangError(message, lineNumber, columnNumber));
            continue;
        }
        // Format 3: "Warning: message"
        match = line.match(/Warning:\s*(.+)/);
        if (match) {
            const message = match[1];
            errors.push(new PohLangError(message, undefined, undefined, 'warning'));
            continue;
        }
        // Generic error if line contains "error" (case insensitive)
        if (line.toLowerCase().includes('error') && line.trim().length > 0) {
            errors.push(new PohLangError(line.trim()));
        }
    }
    return errors;
}
exports.parsePohLangError = parsePohLangError;
//# sourceMappingURL=processUtils.js.map