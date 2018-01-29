export const RadioButton = (props) => (
  <label className="radio-button">{props.label}
    <input type="radio" {...props} />
    <div className="radio-button__indicator"></div>
  </label>
);
