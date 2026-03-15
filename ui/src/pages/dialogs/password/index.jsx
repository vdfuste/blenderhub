 
import { useEffect, useState } from "react";
import "./style.scss";

import TextInput from "@/components/inputs";

const GetPasswordDialog = ({ version, title, text, acceptLabel, acceptCallback, setButtons }) => {
	const [passw, setPassw] = useState("");
	const [errorMessage, setErrorMessage] = useState("");

	const handleType = event => {
		setPassw(event.target.value);
	};

	const handleCheckPassw = async handleClose => {
		setButtons(buttons => {
			const accept = {
				...buttons.accept,
				label: "Loading...",
			};

			return ({ ...buttons, accept });
		});
		
		const isValid = await window.pywebview.api.check_passw(passw);

		if(isValid) {
			handleClose();
			if(acceptCallback) acceptCallback(version, passw);
		}
		else {
			setPassw("");
			setErrorMessage("Incorrect password. Try again.");
		}
	};
	
	useEffect(() => {
		setButtons(buttons => {
			const accept = {
				...buttons.accept,
				label: acceptLabel,
				onClick: handleClose => handleCheckPassw(handleClose),
				disabled: passw === "",
			};

			return ({ ...buttons, accept });
		});
	}, [passw]);
	
	return (
		<div className="input-password">
			<h2>{title}</h2>
			<p>{text}</p>
			{errorMessage && <p className="error-message">{errorMessage}</p>}
			<TextInput
				value={passw}
				placeholder="Password"
				onChange={handleType}
				password />
		</div>
	);
};

export default GetPasswordDialog;
