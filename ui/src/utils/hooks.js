import { useEffect } from "react";

export const useClickOutside = (ref, onClick) => {
	useEffect(() => {
		const handleClickOutside = event => {
			if(!ref.current?.contains(event.target)) onClick(event);
		};

		document.addEventListener("mousedown", handleClickOutside);

		return () => document.removeEventListener("mousedown", handleClickOutside);
	}, [ref, onClick]);
};
