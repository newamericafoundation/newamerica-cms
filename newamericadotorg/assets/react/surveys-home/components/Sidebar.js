import React from 'react';
import CheckboxGroup from './CheckboxGroup';

export default class Sidebar extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    const {
      onFilterChange,
      tags,
      demographics,
      organizations,
    } = this.props;

    return (
      <div className="">
        <div className="sidebar__inner">
          <div>
            <CheckboxGroup
              title="Topics"
              options={tags.map((tag) => ({
                id: tag,
                checked: false,
                label: tag.charAt(0).toUpperCase() + tag.slice(1),
              }))}
              onChange={(filterState) =>
                onFilterChange('tags', filterState)
              }
            />
            <CheckboxGroup
              title="Demographics"
              options={demographics.map((demographic) => ({
                id: demographic,
                checked: false,
                label:
                  demographic.charAt(0).toUpperCase() +
                  demographic.slice(1),
              }))}
              onChange={(filterState) => {
                console.log(filterState);
                onFilterChange('demographics', filterState);
              }}
            />

            {/* <CheckboxGroup
              title="Publication Date"
              options={[
                { checked: false, label: 'Last 3 months', id: 'one' },
                {
                  checked: false,
                  label: 'Last 6 months',
                  id: 'two',
                },
                {
                  checked: false,
                  label: 'Within 1 year',
                  id: 'three',
                },
                {
                  checked: false,
                  label: 'Within 2 year',
                  id: 'four',
                },
                {
                  checked: false,
                  label: '3+ years ago',
                  id: 'five',
                },
              ]}
              onChange={(filterState) =>
                onFilterChange('size', filterState)
              }
            /> */}
            <CheckboxGroup
              title="Sample size"
              options={[
                { checked: false, label: '< 1,000', id: 'one' },
                {
                  checked: false,
                  label: '1,000 - 5,000',
                  id: 'two',
                },
                {
                  checked: false,
                  label: '5,000 - 10,000',
                  id: 'three',
                },
              ]}
              onChange={(filterState) =>
                onFilterChange('size', filterState)
              }
            />
            <CheckboxGroup
              title="Organization"
              options={organizations.map((organization) => ({
                id: organization,
                checked: false,
                label:
                  organization.charAt(0).toUpperCase() +
                  organization.slice(1),
              }))}
              onChange={(filterState) =>
                onFilterChange('organization', filterState)
              }
            />
          </div>
        </div>
      </div>
    );
  }
}
