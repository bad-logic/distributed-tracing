import url from "node:url";

if (import.meta.url === url.pathToFileURL(process.argv[1]).href) {
  console.info("running main application");
}
