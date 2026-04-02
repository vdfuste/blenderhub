import { useContext, useState } from "react";
import "./style.scss";

import { AppContext } from "@/providers/app";
import { OverlayContext } from "@/providers/overlay";
import CreateProjectDialog from "@/pages/dialogs/projects/create";

import { Button, DropdownButton } from"@/components/button";
import Header from "@/components/header";
import List from "@/components/list";

const Buttons = ({ versions, userDocs, type="outline" }) => {
	const { setDialog } = useContext(OverlayContext);

	const formattedVersions = [
		{
			label: `Open Blender ${versions[0]}`,
			value: versions[0]
		},
		{
			title: "More installed versions",
			items: versions.slice(1)
		}
	];

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
	
	const handleOpenBlender = version => {
		window.pywebview.api.open_version(version);
		window.pywebview.api.close_app();
	};

	return (
		<div className="buttons">
			<Button onClick={handleImportProjects} type={type}>
				{type === "outline" ? "Import Projects" : "Add existent projects"}
			</Button>
			{type === "ghost" && <span>or</span>}
			<Button onClick={handleCreateProject} type={type}>
				{type === "outline" ? "New Project" : "Create a new one"}
			</Button>
			{type === "outline" &&
				// <Button onClick={handleOpenBlender}>
				// 	Open Blender {selectedVersion}
				// </Button>
				<DropdownButton
					options={formattedVersions}
					onClick={handleOpenBlender} />
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
			{data?.installedVersions.length > 0 &&
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
