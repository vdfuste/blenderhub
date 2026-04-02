import parse from "class-parser";
import "./style.scss";

import { ContextMenu } from "@/components/menu";
import { OptionsList } from "@/components/dropdown";
import ArrowDown from "@/assets/images/icons/tria-down.svg?react";

export const Button = ({ className, children, onClick, type="filled", disabled=false }) => {
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

export const DropdownButton = ({ className, label, onClick, options=[], disabled=false }) => {
	const handleClick = option => {
		if(!disabled && onClick) onClick(option);
	};

	return (
		<div className="dropdown-button">
			<Button className="label-button" onClick={() => handleClick(options[0].value)}>
				{options[0].label}
			</Button>
			<ContextMenu disabled={disabled}>
				<OptionsList options={options.slice(1)} onClickItem={handleClick} />
				<div className="arrow-button">
					<ArrowDown className="icon" />
				</div>
			</ContextMenu>
		</div>
	);
};
