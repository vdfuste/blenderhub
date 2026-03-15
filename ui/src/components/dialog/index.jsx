import { useState } from "react";
import "./style.scss";

import Button from "@/components/button";

const defaultButtonsConfig = {
	accept: {
		label: "Accept",
		onClick: () => {},
		disabled: false,
	},
	cancel: {
		label: "Cancel",
		onClick: () => {},
		disabled: false,
	}
};

const Dialog = ({ children, data, handleClose }) => {	
	const [{ accept, cancel }, setButtons] = useState({ ...defaultButtonsConfig, ...data.buttons });
	
	const handleOnAccept = () => {
		if(!accept.disabled) accept.onClick(handleClose);
	};
	
	const handleOnCancel = () => {
		if(!cancel.disabled) cancel.onClick();
		handleClose();
	};

	const handleClickOutside = () => {
		//if(!cancel) handleClose();
	};
	
	return (
		<div className="dialog-wrapper" onClick={handleClickOutside}>
			<div className="dialog">
				{data?.content(setButtons) || children}
				<div className="dialog-buttons">
					{cancel &&
						<Button
							type="outline"
							onClick={handleOnCancel}
							disabled={cancel.disabled}
						>
							{cancel.label}
						</Button>
					}
					<Button
						onClick={handleOnAccept}
						disabled={accept.disabled}
					>
						{accept.label}
					</Button>
				</div>
			</div>
		</div>
	);
};

export default Dialog;
