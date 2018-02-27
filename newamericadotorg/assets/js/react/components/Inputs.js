export const RadioButton = (props) => (
  <label className="radio-button">{props.label}
    <input type="radio" {...props} />
    <div className="radio-button__indicator"></div>
  </label>
);


export const CheckBox = (props) => (
  <label className="checkbox">{props.label}
    <input type="checkbox" {...props} />
    <div className="checkbox__indicator"></div>
  </label>
);

export const Text = ({ children, ...props}) => (
  <div className="input">
    <input type="text" required {...props} />
    <label className="input__label button--text">{props.label}</label>
    {children}
  </div>
);

export const TextArea = ({ children, ...props}) => (
  <div className="input">
    <textarea type="text" rows="4" required {...props} />
    <label className="input__label button--text">{props.label}</label>
    {children}
  </div>
);
