import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import vitePluginSvgr from "vite-plugin-svgr";
import path from "path";

// https://vite.dev/config/
export default defineConfig({
	plugins: [react(), vitePluginSvgr()],
	base: "./",
	resolve: {
		alias: {
			"@": path.resolve(__dirname, "./src")
		}
	},
	build: {
		outDir: "dist"
	}
});
