#!/usr/bin/env node
const { spawnSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const packageRoot = findPackageRoot();
const binary = findPlatformPackageBinary();

if (!binary) {
  const packageName = platformPackageName();
  const version = packageVersion();
  console.error("docx-kit: platform package is missing.");
  console.error(
    packageName
      ? `docx-kit: expected optional dependency ${packageName} to provide the binary.`
      : `docx-kit: unsupported platform ${process.platform}/${process.arch}.`,
  );
  if (packageName) {
    console.error(`docx-kit: run "npm install -g @dztabel/docxkit@${version} ${packageName}@${version}".`);
  }
  process.exit(1);
}

const result = spawnSync(binary, process.argv.slice(2), {
  cwd: process.cwd(),
  env: process.env,
  stdio: "inherit",
});

if (result.error) {
  console.error(`docx-kit: failed to start: ${result.error.message}`);
  process.exit(1);
}

process.exit(result.status ?? 1);

function findPackageRoot() {
  const candidates = [
    path.resolve(__dirname, ".."),
    path.resolve(__dirname, "node_modules", "@dztabel", "docxkit"),
    path.resolve(__dirname, "..", "node_modules", "@dztabel", "docxkit"),
  ];

  for (const candidate of candidates) {
    if (isDocxKitPackageRoot(candidate)) {
      return candidate;
    }
  }

  try {
    const packageJson = require.resolve("@dztabel/docxkit/package.json", {
      paths: [__dirname, process.cwd()],
    });
    return path.dirname(packageJson);
  } catch (_) {
    return path.resolve(__dirname, "..");
  }
}

function isDocxKitPackageRoot(candidate) {
  try {
    const packageJson = JSON.parse(fs.readFileSync(path.join(candidate, "package.json"), "utf8"));
    return packageJson.name === "@dztabel/docxkit" && fs.existsSync(path.join(candidate, "npm", "docx-kit.cjs"));
  } catch (_) {
    return false;
  }
}

function findPlatformPackageBinary() {
  const packageName = platformPackageName();
  if (!packageName) {
    return null;
  }
  try {
    const packageJson = require.resolve(`${packageName}/package.json`, { paths: [packageRoot] });
    const platformRoot = path.dirname(packageJson);
    const candidate = path.join(platformRoot, process.platform === "win32" ? "docx-kit.exe" : "docx-kit");
    return fs.existsSync(candidate) ? candidate : null;
  } catch (_) {
    return null;
  }
}

function platformPackageName() {
  const arch = process.arch === "arm64" ? "arm64" : process.arch === "x64" ? "x64" : null;
  if (!arch) {
    return null;
  }
  if (process.platform === "darwin") {
    return `@dztabel/docxkit-darwin-${arch}`;
  }
  if (process.platform === "win32" && arch === "x64") {
    return "@dztabel/docxkit-win32-x64";
  }
  return null;
}

function packageVersion() {
  try {
    const packageJson = JSON.parse(fs.readFileSync(path.join(packageRoot, "package.json"), "utf8"));
    return packageJson.version || "latest";
  } catch (_) {
    return "latest";
  }
}
