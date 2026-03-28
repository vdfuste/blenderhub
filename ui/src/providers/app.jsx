/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useEffect, useState } from "react";

import { OverlayContext } from "./overlay";
import GetPasswordDialog from "@/pages/dialogs/password";
import InstallingDialog from "@/pages/dialogs/installing";
import RemovingDialog from "@/pages/dialogs/removing";

export const AppContext = createContext();

const AppProvider = ({ children }) => {
	const { setDialog } = useContext(OverlayContext);
	const [data, setData] = useState(null);

	const handleOpenPasswDialog = data => {
		setDialog({
			content: setButtons => (
				<GetPasswordDialog
					{...data}
					acceptCallback={window.pywebview.api[data.execApi]}
					setButtons={setButtons} />
			)
		});
	};

	const handleOpenInstallDialog = data => {
		setDialog({
			content: setButtons => <InstallingDialog {...data} setButtons={setButtons} />,
			buttons: {
				accept: {
					label: "Cancel installation"
				},
				cancel: null
			}
		});
	};
	
	const handleOpenRemoveDialog = data => {
		setDialog({
			content: setButtons => <RemovingDialog {...data} setButtons={setButtons} />,
			buttons: {
				accept: {
					label: "Removing...",
					disabled: true,
				},
				cancel: null
			}
		});
	};
	
	useEffect(() => {
		window.getPassword = data => handleOpenPasswDialog(data);
		window.installVersion = data => handleOpenInstallDialog(data);
		window.removeVersion = data => handleOpenRemoveDialog(data);
		window.updateData = newData => setData(newData);
		window.addEventListener("pywebviewready", async () => {
			const response = await window.pywebview.api.get_init_data();
			setData(JSON.parse(response));
		});
	}, []);

	return (
		<AppContext.Provider value={{ data, setData }}>
			{children}
		</AppContext.Provider>
	);
};

export default AppProvider;
