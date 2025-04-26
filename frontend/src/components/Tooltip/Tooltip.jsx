import PropTypes from "prop-types";
import "./Tooltip.css";

//To lazy to refactor the allready used tooltips So,.. there you have it!

const Tooltip = ({ children, tooltipText, position = "top", onClick }) => {
  return (
    <div
      className={`tooltip_component tooltip-${position}_component`}
      onClick={onClick}
    >
      {children}
      <span className="tooltiptext_component">{tooltipText}</span>
    </div>
  );
};

Tooltip.propTypes = {
  children: PropTypes.node.isRequired, // The content inside the tooltip (e.g., an icon)
  tooltipText: PropTypes.string.isRequired, // The text to display in the tooltip
  position: PropTypes.oneOf(["top", "right", "bottom", "left"]), // Tooltip position
  onClick: PropTypes.func, // Optional click handler for the tooltip
};

export default Tooltip;
