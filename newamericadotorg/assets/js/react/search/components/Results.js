import { Response } from '../../components/API';
import { Component } from 'react';
import { NAME } from '../constants';

class Results extends Component {

  render(){
    let { response: { results }} = this.props;
    return(
      <div className="search__results">
        {results.map((p,i)=>(
          <h4>{p.title}</h4>
        ))}
      </div>
    );
  }
}

const ResultsWrapper = () => (
  <Response name={NAME} component={Results} />
);

export default ResultsWrapper;
