import { useEffect, useState } from "react";
import "./style.scss";

import ProgressBar from "@/components/progress";

const ImportingDialog = ({ title, setButtons }) => {
	const [process, setProcess] = useState(window.pywebview.state.import_process);

	useEffect(() => {
		const intervalId = setInterval(() => {
			setProcess(() => window.pywebview.state.import_process);
		}, 1000);
		
		setButtons(buttons => {
			const accept = {
				...buttons.accept,
				onClick: handleClose => {
					handleClose();
				}
			};

			return ({ ...buttons, accept });
		});

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
					}
				};

				return ({ ...buttons, accept });
			});
		}
	}, [process]);
	
	return (
		<div className="installing">
			<h2>{title}</h2>
			<ProgressBar {...process} />
		</div>
	);
};

export default ImportingDialog;
