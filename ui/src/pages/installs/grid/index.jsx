import { useState } from "react";
import { useOutletContext, useParams } from "react-router";
import "./style.scss";

import { Dropdown } from "@/components/dropdown";
import { Button } from"@/components/button";

const URL_IMAGES = "https://www.blender.org/wp-content/uploads/";

const VersionCard = ({ version, subversions, urlImage, lts=false }) => {
	const firstSelectionIndex = subversions[0].items.length > 0 ? 0 : 1;
	const [selected, setSelected] = useState(subversions[firstSelectionIndex].items[0]);
	const isInstalled = subversions[1].items.includes(selected);
	const dropdownSubversions = subversions.filter(s => s.items.length !== 0);
	
	const hanldeInstallRemove = () => {
		if(isInstalled) window.pywebview.api.remove_version(selected);
		else window.pywebview.api.install_version(selected);
	};
	
	return (
		<div className="version-card" style={{ backgroundImage: `url(${URL_IMAGES}${urlImage})` }}>
			<div className="card-content">
				<div className="version">
					<span className="version-text">
						{version}{lts && " LTS"}
					</span>
				</div>
				<div className="row">
					<div className="install-button">
						<Dropdown
							selected={selected}
							options={dropdownSubversions}
							onChange={setSelected} />

						<Button onClick={hanldeInstallRemove}>
							{isInstalled ? "Remove" : "Install"} Blender {selected}
						</Button>
					</div>
				</div>
			</div>
		</div>
	);
};

const GridInstallsSubPage = () => {
	const { serie } = useParams();
	const versions = useOutletContext();

	const selectedSerie = versions[serie];

	return (
		<div className="grid-installs">
			{selectedSerie.map(data => <VersionCard {...data} key={data.version} />)}
			<div className="filler"></div>
			<div className="filler"></div>
			<div className="filler"></div>
			<div className="filler"></div>
		</div>
	);
};

export default GridInstallsSubPage;
