import { useContext } from "react";
import { NavLink, Outlet } from "react-router";
import "./style.scss";

import { AppContext } from "@/providers/app";
import Header from "@/components/header";

const InstallsPage = () => {
	const { releases } = useContext(AppContext).data;
	const { series, allVersions } = releases;

	const splittedVersions = { all: allVersions };
	const tabs = [{ path: "all", label: "All"}];

	const labelize = value => `${value[0].toUpperCase()}${value.slice(1).replace("-", " ")}`;
	
	Object.entries(series).forEach(([serie, indexes]) => {
		splittedVersions[serie] = indexes.map(index => allVersions[index]);
		tabs.push({
			path: serie,
			label: labelize(serie)
		});
	});

	return <>
		<Header title="Installs">
			<nav className="tabs">
				{tabs.map(tab => (
					<NavLink
						className="tab"
						to={tab.path}
						key={tab.path}
					>
						{tab.label}
					</NavLink>
				))}
			</nav>
		</Header>
		<Outlet context={splittedVersions} />
	</>;
};

export default InstallsPage;
