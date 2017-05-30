import { Component } from 'react';
import PropTypes from 'prop-types';

export default class Select extends Component {
  static propTypes = {
    options: PropTypes.array.required,
    defaultOption: PropTypes.object,
    name: PropTypes.string,
    className: PropTypes.string,
    onChange: PropTypes.func,
    valueAccessor: PropTypes.string,
    labelAccessor: PropTypes.string
  }

  static defaultProps = {
    onChange: ()=>{},
    valueAccessor: 'value',
    labelAccessor: 'label'
  }

  constructor(props) {
    super(props);

    this.state = {
      selectedValue: '',
      selectedLabel: '',
      expanded: false
    }
  }

  setValue = (option) => {
    let { onChange, valueAccessor, labelAccessor } = this.props;
    this.setState({
      selectedValue: option[valueAccessor],
      selectedLabel: option[labelAccessor],
      expanded: false
    });
    onChange(option);
  }

  toggleExpand = () => {
    let { expanded } = this.state;
    this.setState({
      expanded: !expanded
    });
  }

  blur = () => {
    this.setState({
      expanded: false
    });
  }

  clear = () => {
    let { onChange } = this.props;
    this.setState({
      selectedValue: '',
      selectedLabel: '',
      expanded: false
    });
    onChange(null);
  }

  render(){
    let { selectedValue, selectedLabel, expanded } = this.state;
    let { name, className, options, defaultOption, labelAccessor } = this.props;

    let label = selectedLabel=='' && defaultOption ? defaultOption[labelAccessor] : selectedLabel;
    let classes = `${expanded ? 'expanded' : ''} ${className ? className : ''}`;

    return (
      <div tabIndex="1" onBlur={this.blur} className={`select ${classes}`}>
        <div className="select__input-wrapper" onClick={this.toggleExpand}>
          <label className="select__label active">{name}</label>
          <input ref={(el)=>{ this.input=el;}} disabled value={label} className="select__input" />
        </div>
        <span className="select__clear" onClick={this.clear}>
          <i className="fa fa-times"></i>
        </span>
        <span className="select__arrow" onClick={this.toggleExpand}>
          <i className="fa fa-chevron-down"></i>
        </span>
        <div className="select__options">
          {options.map((o,i)=>(
            <span onClick={()=>{this.setValue(o)}}
              className={`select__options__option ${label===o[labelAccessor] ? 'selected' : ''}`}>
              {o[labelAccessor]}
            </span>
          ))}
        </div>
      </div>
    );
  }
}
