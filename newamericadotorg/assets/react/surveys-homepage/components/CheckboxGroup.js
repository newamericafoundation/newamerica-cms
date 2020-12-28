import React from 'react';
import './CheckboxGroup.scss';

class CheckboxGroup extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isOpen: false,
    };

    this.props.options.forEach((val) => {
      this.state[val.id] = val.checked ? true : false;
    });
  }

  handleChange = (e) => {
    this.setState(
      {
        [e.target.id]: e.target.checked,
      },
      () => this.props.onChange(this.state)
    );
  };

  toggleCheckboxGroup = () => {
    this.setState({ isOpen: !this.state.isOpen });
  };

  render() {
    const { isOpen } = this.state;
    const { options, title } = this.props;
    const _options = options.filter((item) => {
      return item.id !== 'isOpen';
    });

    return (
      <div className="checkbox__container">
        <span
          className={`${
            isOpen ? 'margin-bottom-25' : ''
          } checkbox__group-title`}
          onClick={this.toggleCheckboxGroup}
        >
          {title}
          <i className={`fa fa-${isOpen ? 'times' : 'plus'}`}></i>
        </span>
        {isOpen &&
          _options.map((option, i) => (
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
