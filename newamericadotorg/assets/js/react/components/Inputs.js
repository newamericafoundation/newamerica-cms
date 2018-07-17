export const RadioButton = (props) => (
  <div className="inline radio-button">
    <label htmlFor={props.name} className="margin-0">
      <h6 className="inline">{props.label}</h6>
    </label>
    <input type="radio" {...props} />
    <div className="radio-button__indicator"></div>
  </div>
);


export const CheckBox = (props) => (
  <div className="checkbox">
    <label htmlFor={props.name} className="margin-0">
      <h6 className="inline">{props.label}</h6>
    </label>
    <input type="checkbox" {...props} />
    <div className="checkbox__indicator"></div>
  </div>
);

export const Text = ({ children, ...props}) => (
  <div className="input">
    <input type="text" required {...props} />
    <label className="input__label" htmlFor={props.name}>
      <h5 className="margin-0">{props.label}</h5></label>
    {children}
  </div>
);

export const TextArea = ({ children, ...props}) => (
  <div className="input">
    <textarea type="text" rows="4" required {...props} />
    <label className="input__label" htmlFor={props.name}>
      <h5 className="margin-0">{props.label}</h5>
    </label>
    {children}
  </div>
);
