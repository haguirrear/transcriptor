import * as esbuild from "esbuild";

await esbuild.build({
  entryPoints: ["./frontend/index.ts"],
  bundle: true,
  outfile: "./static/js/base.js",
  minify: true,
  target: ["es2016", "chrome58", "edge16", "firefox57", "safari11"],
});
