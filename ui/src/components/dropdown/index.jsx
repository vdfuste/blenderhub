import { useRef, useState } from "react";
import parse from "class-parser";
import "./style.scss";

import { ContextMenu } from "@/components/menu";
import ArrowDown from "@/assets/images/icons/tria-down.svg?react";

const OptionsList = ({ options, onClickItem }) => {
	return (
		<div className="menu-list">
			{options.map(({ title, items }, index) => {
				return <ul className="list-section" key={index}>
					{title && <span className="list-title">{title}</span>}
					{items.map((option, i) => {
						return (
							<li
								className="list-item"
								onClick={() => onClickItem(option)}
								key={index + "_" + i}
							>
								{option}
							</li>
						);
					})}
				</ul>;
			})}
		</div>
	);
};

const Dropdown = ({ className, selected, onChange, options=[], disabled=false }) => {	
	return (
		<ContextMenu
			className={parse("dropdown", className)}
			disabled={disabled}
		>
			<OptionsList options={options} onClickItem={onChange} />
			<div className="dropdown-header">
				<div className="content">
					{selected}
				</div>
				<ArrowDown className="icon" />
			</div>
		</ContextMenu>
	);
};

export default Dropdown;
