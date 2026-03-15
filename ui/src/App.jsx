import { Navigate, Route, Routes } from "react-router";
import "./App.scss";

import AppProvider from "./providers/app";
import OverlayProvider from "./providers/overlay";

import Sidebar from "./components/sidebar";
import ProjectsPage from "./pages/projects";
import InstallsPage from "./pages/installs";
import GridInstallsSubPage from "./pages/installs/grid";
import ConfigPage from "./pages/config";

function App() {
	return (
		<OverlayProvider>
			<AppProvider>
				<Sidebar />
				<main>
					<Routes>
						<Route index element={<Navigate to="projects" replace />} />
						<Route path="projects" element={<ProjectsPage />} />
						<Route path="installs" element={<InstallsPage />}>
							<Route index element={<Navigate to="all" replace />} />
							<Route path=":serie" element={<GridInstallsSubPage />} />
						</Route>
						<Route path="config" element={<ConfigPage />} />
					</Routes>
				</main>
			</AppProvider>
		</OverlayProvider>
	);
}

export default App;
