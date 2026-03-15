/* eslint-disable react-refresh/only-export-components */
import { createContext, useState } from "react";
import Dialog from "@/components/dialog";

export const OverlayContext = createContext();

const OverlayProvider = ({ children }) => {
	const [dialog, setDialog] = useState(null);

	return (
		<OverlayContext.Provider value={{ setDialog }}>
			{children}
			{dialog &&
				<Dialog
					data={dialog}
					handleClose={() => setDialog(null)} />
			}
		</OverlayContext.Provider>
	);
};

export default OverlayProvider;
