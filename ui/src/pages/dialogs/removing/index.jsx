import { useEffect, useState } from "react";
import "./style.scss";

import ProgressBar from "@/components/progress";

const RemovingDialog = ({ title, setButtons }) => {
	const [process, setProcess] = useState(window.pywebview.state.remove_process);

	useEffect(() => {
		const intervalId = setInterval(() => {
			setProcess(() => window.pywebview.state.remove_process);
		}, 200);

		return () => clearInterval(intervalId);
	}, []);

	useEffect(() => {
		if(process.percent === 100) {
			setButtons(buttons => {
				const accept = {
					...buttons.accept,
					label: "Close",
					onClick: handleClose => {
						window.pywebview.api.refresh_ui();
						handleClose();
					},
					disabled: false
				};

				return ({ ...buttons, accept });
			});
		}
	}, [process]);
	
	return (
		<div className="removing">
			<h2>{title}</h2>
			<ProgressBar {...process} />
		</div>
	);
};

export default RemovingDialog;
