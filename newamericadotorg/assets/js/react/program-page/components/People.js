import { NAME } from '../constants';
import { Component } from 'react';
import { Fetch } from '../../components/API';
import { Person, PersonsList } from '../../components/People'
import Image from '../../components/Image';

export default class People extends Component {
  render(){
    let { program, programType } = this.props;
    return (
      <Fetch name={`${NAME}.people`}
        endpoint="author"
        component={PersonsList}
        fetchOnMount={true}
        initialQuery={{
          [programType == 'program' ? 'program_id' : 'subprogram_id']: program.id,
          limit: 100
        }}/>
    );
  }
}
