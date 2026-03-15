import parse from "class-parser";
import "./style.scss";

const Button = ({ className, children, onClick, type="filled", disabled=false }) => {
	const handleClick = event => {
		if(!disabled && onClick) onClick(event);
	};
	
	return (
		<button
			className={parse("button", className, type)}
			onClick={handleClick}
			disabled={disabled}
		>
			{children}
		</button>
	);
};

export default Button;
