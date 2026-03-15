import parse from "class-parser";
import "./style.scss";

const TextInput = ({ disabled, password, ...rest }) => {	
	return (
		<div className={parse("text-input", { disabled })}>
			<input type={password ? "password" : "text"} {...rest} />
		</div>
	);
};

export default TextInput;
