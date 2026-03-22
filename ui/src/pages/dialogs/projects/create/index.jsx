 
import { useEffect, useState } from "react";
import "./style.scss";

import TextInput from "@/components/inputs";
import Dropdown from "@/components/dropdown";
import Button from "@/components/button";

import Folder from "@/assets/images/icons/folder.svg?react";

const CreateProjectDialog = ({ data }) => {
	const { setButtons, versions, userDocs } = data;
	const [newProject, setNewProject] = useState({
		filename: "",
		path: userDocs,
		version: versions[0]
	});

	const dropdownVersions = [{
		title: "Installed versions",
		items: versions
	}];

	useEffect(() => {
		setButtons(buttons => {
			const accept = {
				...buttons.accept,
				onClick: handleClose => {
					window.pywebview.api.create_new_project(newProject);
					handleClose();
				},
				disabled: newProject.filename === "",
			};

			return ({ ...buttons, accept });
		});
	}, [newProject]);
	
	const handleChange = (value, element) => {
		setNewProject(prev => ({ ...prev, [element]: value }));
	};

	const handleSelectLocation = async () => {
		const path = await window.pywebview.api.get_folder_location(newProject.path);
		if(path) setNewProject(prev => ({ ...prev, path }));
	};
	
	return (
		<div className="new-project">
			<h2>Create a new project</h2>
			
			<div className="row">
				<TextInput
					className="filename"
					value={newProject.filename}
					placeholder="Project Name"
					onChange={event => handleChange(event.target.value, "filename")} />
			
				<Dropdown
					className="version"
					selected={newProject.version}
					options={dropdownVersions}
					onChange={option => handleChange(option, "version")} />
			</div>

			<div className="row">
				<TextInput
					value={newProject.path}
					placeholder="Location"
					onChange={event => handleChange(event.target.value, "path")} />
				
				<Button onClick={handleSelectLocation} type="outline">
					<Folder />
					<span>Browse...</span>
				</Button>
			</div>
			
		</div>
	);
};

export default CreateProjectDialog;
