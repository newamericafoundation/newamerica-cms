// import { DateRangePicker, toMomentObject } from 'react-dates';
import { Component } from 'react';

class Picker extends Component {
  constructor(props){
    super(props);
    this.state = {
      startDate: toMomentObject(props.startDate),
      endDate: toMomentObject(props.endDate)
    };
  }

  render(){
    return null; //(
      // <DateRangePicker
      //   className={this.props.className}
      //   onDatesChange={({startDate, endDate})=>{
      //     this.setState({startDate, endDate});
      //     this.props.onDatesChange({
      //       startDate: startDate ? startDate.format('YYYY-MM-DD') : '',
      //       endDate: endDate ? endDate.format('YYYY-MM-DD') : ''
      //     });
      //   }}
      //   showClearDates={true}
      //   isOutsideRange={(()=>(false))}
      //   startDate={this.state.startDate}
      //   endDate={this.state.endDate}
      //   focusedInput={this.state.focusedInput}
      //   onFocusChange={(focusedInput)=>{this.setState({focusedInput})}}
      // />
    //);
  }
}

export default Picker;
