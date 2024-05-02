import * as esbuild from "esbuild";

// Configure output directory
const outputDir = "./static/dist";

// Define entry points for different pages
const entryPoints = {
  base: "./frontend/src/base.ts",
  home: "./frontend/src/home.ts",
  login: "./frontend/src/login.ts",
  // frontend: "./frontend/index.ts"
};

async function build() {
  try {
    await esbuild.build({
      entryPoints: entryPoints,
      bundle: true,
      minify: true,
      outdir: outputDir,
      format: "esm",
      sourcemap: true,
      // target: ["es2018", "chrome58", "edge18", "firefox57", "safari11"],
      target: ["es2018"],
      // watch: process.argv.includes("--watch") && {
      //   onRebuild(error, result) {
      //     if (error) console.error("Build failed:", error);
      //     else console.log("Build succeeded:", result);
      //   },
      // },
    });
  } catch (error) {
    console.log("Build failed:", error);
  }
}

await build();
