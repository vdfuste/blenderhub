import { useContext, useState } from "react";
import "./style.scss";

import { AppContext } from "@/providers/app";
import { OverlayContext } from "@/providers/overlay";
import CreateProjectDialog from "@/pages/dialogs/projects/create";

import Button from "@/components/button";
import Header from "@/components/header";
import List from "@/components/list";

const Buttons = ({ versions, userDocs, type="outline" }) => {
	const { setDialog } = useContext(OverlayContext);
	const [selectedVersion, setSelectedVersion] = useState(versions[0]);

	const handleImportProjects = () => {
		window.pywebview.api.import_projects();
	};
	
	const handleCreateProject = () => {
		setDialog({
			content: setButtons => <CreateProjectDialog data={{ setButtons, versions, userDocs }} />,
			buttons: {
				accept: {
					label: "Create new project",
				}
			}
		});
	};
	
	const handleOpenBlender = () => {
		window.pywebview.api.open_version(selectedVersion);
		window.pywebview.api.close_app();
	};

	return (
		<div className="buttons">
			<Button onClick={handleImportProjects} type={type}>
				{type === "outline" ? "Add Existent Project" : "Add an existent project"}
			</Button>
			{type === "ghost" && <span>or</span>}
			<Button onClick={handleCreateProject} type={type}>
				{type === "outline" ? "Create New Project" : "Create a new project"}
			</Button>
			{type === "outline" &&
				<Button onClick={handleOpenBlender}>
					Open Blender {selectedVersion}
				</Button>
			}
		</div>
	);
};

const ProjectsPage = () => {
	const { data, setData } = useContext(AppContext);
	
	const handleUpdateItems = items => {
		setData(() => ({ ...data, projects: items }));
	};

	return <>
		<Header title="Projects">
			{data && data.installedVersions &&
				<Buttons
					versions={data.installedVersions}
					userDocs={data.userDocs} />
			}
		</Header>
		{data &&
			<List
				items={data.projects}
				versions={data.installedVersions}
				onChange={handleUpdateItems}
				buttons={
					<Buttons
						versions={data.installedVersions}
						userDocs={data.userDocs}
						type="ghost" />
				} />
		}
	</>;
};

export default ProjectsPage;
