import "./style.scss";

const ProgressBar = ({ percent, feedback }) => {
	return (
		<div className="progress-bar">
			<div className="feedback-text">
				<span>{feedback}{percent < 100 && "..."}</span>
				<span className="percent">
					{percent}%
				</span>
			</div>
			<div className="bar">
				<div className="progress" style={{ width: `${percent}%` }} />
			</div>
		</div>
	);
};

export default ProgressBar;
