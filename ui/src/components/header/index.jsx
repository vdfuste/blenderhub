import "./style.scss";

const Header = ({ children, title }) => {
	return (
		<header className="header">
			<h2>{title}</h2>
			{children}
		</header>
	);
};

export default Header;
