import React from 'react';
import './CheckboxGroup.scss';

class CheckboxGroup extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};

    this.props.options.forEach((val) => {
      this.state[val.id] = val.checked ? true : false;
    });
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(e) {
    this.setState(
      {
        [e.target.id]: e.target.checked,
      },
      () => this.props.onChange(this.state)
    );
  }

  render() {
    const { options, title } = this.props;

    return (
      <div className="checkbox__container">
        <span className="checkbox__group-title">{title}</span>
        {options.map((option, i) => (
          <div className="checkbox-group__options" key={i}>
            <input
              id={option.id}
              type="checkbox"
              checked={this.state[option.id]}
              onChange={this.handleChange}
            />
            <label htmlFor={option.id} className="checkbox__label">
              {option.label}
            </label>
          </div>
        ))}
      </div>
    );
  }
}

export default CheckboxGroup;
