 
import { useEffect, useState } from "react";
import "./style.scss";

import TextInput from "@/components/inputs";
import { Dropdown } from "@/components/dropdown";
import { Button } from"@/components/button";

import Folder from "@/assets/images/icons/folder.svg?react";

const DeleteProjectDialog = () => {	
	return (
		<div className="new-project">
			<h2>Delete project from the computer</h2>
			<p>Are you sure that you want to delete this project? This action will erase the project file from your computer permanently.</p>
			<p>If you just want to remove the project from the list of this app and keep the original file please use the "Remove from the list" option.</p>
		</div>
	);
};

export default DeleteProjectDialog;
