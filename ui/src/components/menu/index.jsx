import { useRef, useState } from "react";
import parse from "class-parser";
import "./style.scss";

import { useClickOutside } from "@/utils/hooks";

const Menu = ({ className, children }) => {
	return (
		<div className={parse("menu", className)}>
			{children}
		</div>
	);
};

const DefaultItem = ({ content, onClick }) => {	
	return (
		<li className="list-item" onClick={onClick}>
			{content}
		</li>
	);
};

export const MenuList = ({ options, Item=DefaultItem }) => {
	return (
		<div className="menu-list">
			{options.map(({ title, items }, index) => {
				return (
					<ul className="list-section" key={index}>
						{title && <span className="list-title">{title}</span>}
						{items.map((item, i) => <Item {...item} key={index + "_" + i} />)}
					</ul>
				);
			})}
		</div>
	);
};

export const ContextMenu = ({ className, children, disabled }) => {
	const [open, setOpen] = useState(false);
	const ref = useRef(null);

	useClickOutside(ref, () => setOpen(false));

	const [menuContent, ...content] = children;
	
	const handleOpen = event => {
		event.stopPropagation();
		setOpen(!open && !disabled);
	};

	return (
		<div
			className={parse("context-menu", className, { open })}
			ref={ref}
			onClick={handleOpen}
			onBlur={() => setOpen(false)}
			disabled={disabled}
			tabIndex={0}
		>
			{content}
			{open && <Menu>{menuContent}</Menu>}
		</div>
	);
};

export default Menu;
