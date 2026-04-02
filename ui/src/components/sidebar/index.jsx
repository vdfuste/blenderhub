import { useState } from "react";
import { NavLink } from "react-router";
import "./style.scss";

import Folder from "@/assets/images/icons/folder.svg?react";
import Installs from "@/assets/images/icons/download.svg?react";
import Properties from "@/assets/images/icons/properties.svg?react";

const Sidebar = () => {
	const [open, setOpen] = useState(true);

	const routes = [
		{
			path: "/projects",
			label: "Projects",
			icon: () => <Folder />,
		},
		{
			path: "/installs",
			label: "Installs",
			icon: () => <Installs />,
		},
		/*{
			path: "/config",
			label: "Config Files",
			icon: () => <Properties />,
		},*/
	];

	return (
		<aside className="sidebar">
			<h1>Blender Hub</h1>
			<nav>
				{routes.map(route => (
					<NavLink
						className="route"
						to={route.path}
						key={route.label}
					>
						<div className="decorator"></div>
						{route.icon()}
						{/* <img className="icon" src={`/images/icons/${route.icon}`} /> */}
						<span className="label">{route.label}</span>
					</NavLink>
				))}
			</nav>
		</aside>
	);
};

export default Sidebar;
