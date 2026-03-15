import { useContext } from "react";
import "./style.scss";

import { OverlayContext } from "@/providers/overlay";
import DeleteProjectDialog from "@/pages/dialogs/projects/delete";

import { ContextMenu, MenuList } from "@/components/menu";
import Dropdown from "@/components/dropdown";
import Button from "@/components/button";

import Bookmark from "@/assets/images/icons/bookmark.svg?react";
import ThreeDotsIcon from "@/assets/images/icons/three-dots.svg?react";

const EmptyList = ({ children }) => {
	return (
		<div className="empty-list">
			No projects found. {children}
		</div>
	);
};

const Item = ({ data, onChange, versions }) => {
	const { setDialog } = useContext(OverlayContext);

	const { filename, version, path, modified } = data;
	
	const formattedFilename = filename.replace(".blend", "");
	const formattedDate = (new Date(modified)).toLocaleDateString();
	
	const dropdownVersions = [
		{
			title: "",
			items: [version]
		},
		{
			title: "Installed versions",
			items: versions.filter(v => v !== version)
		}
	];

	const handleOpenProject = () => {
		window.pywebview.api.open_project(data);
	};

	const handleSelectVersion = selectedVersion => {
		onChange({ ...data, version: selectedVersion });
	};

	const handleDeleteProject = () => {
		setDialog({
			content: () => <DeleteProjectDialog />,
			accept: {
				label: "Delete project from computer",
				onClick: () => window.pywebview.api.remove_project(data, true)
			},
		});
	};

	const optionsMenu = [{
		items: [
			{
				content: "Remove project from the list",
				onClick: () => window.pywebview.api.remove_project(data)
			},
			{
				content: "Delete project from computer",
				onClick: handleDeleteProject,
			},
		]
	}];
	
	return (
		<li className="item">
			<div className="item-space"></div>
			{/* <div className="item-star">
				<Bookmark />
			</div> */}
			<div className="item-name" onClick={handleOpenProject}>
				<span className="filename">
					{formattedFilename}
				</span>
				<span className="filepath">
					{path}
				</span>
			</div>
			<div className="item-modified" onClick={handleOpenProject}>
				{formattedDate}
			</div>
			<div className="item-version">
				<Dropdown
					options={dropdownVersions}
					selected={version}
					onChange={handleSelectVersion} />
				
				<ContextMenu>
					<MenuList options={optionsMenu} />
					<div className="item-options">
						<ThreeDotsIcon />
					</div>
				</ContextMenu>
			</div>
			<div className="item-space"></div>
		</li>
	);
};

const List = ({ items, versions, onChange, buttons }) => {	
	const handleSetItem = (data, index) => {
		const newItems = [...items];
		newItems[index] = data;

		onChange(newItems);
	};
	
	return (
		<div className="list">
			<div className="list-header">
				<div className="header-space"></div>
				{/* <button className="header-star">
						<Bookmark />
					</button> */}
				<button className="header-name">Name</button>
				<button className="header-modified">Last Modified</button>
				<button className="header-version">Version</button>
				<div className="header-space"></div>
			</div>
			{!items.length ?
				<EmptyList>{buttons}</EmptyList> :
				<ul className="items">
					{items.map((item, index) => 
						<Item
							data={item}
							onChange={data => handleSetItem(data, index)}
							versions={versions}
							key={index} />
					)}
				</ul>
			}
		</div>
	);
};

export default List;
