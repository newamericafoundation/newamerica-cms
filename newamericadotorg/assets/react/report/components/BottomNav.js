import "./BottomNav.scss";

import { Link } from "react-router-dom";
import React, { Component } from "react";

import { Home } from "../../components/Icons";

const Tooltip = ({ content, activeIndex, numSections }) => (
  <div className={`report__bottom-nav__tooltip`}>
    <h6 className="paragraph white margin-0">{content.title}</h6>
    <div
      className="report__bottom-nav__tooltip__caret"
      style={{
        right:
          numSections * 40 - (content.index - activeIndex + 1) * 40 + 5 ||
          "calc(50% + 10px)"
      }}
    />
  </div>
);

class BottomNavButtons extends Component {
  render() {
    let { section, report } = this.props;
    if (!section) section = { number: 0 };
    let next = report.sections[section.number],
      previous = report.sections[section.number - 2];

    return (
      <div className="report__bottom-nav">
        <div className="container">
          {previous && (
            <div className="report__bottom-nav__button previous">
              <Link
                to={`${report.url}${previous.slug}/`}
                className="button with-caret--left"
              >
                Prev. Section
              </Link>
            </div>
          )}
          {section.number === 1 && (
            <div className="report__bottom-nav__button previous">
              <Link to={`${report.url}`} className="button with-caret--left">
                Home
              </Link>
            </div>
          )}
          {next && (
            <div className="report__bottom-nav__button next">
              <Link
                to={`${report.url}${next.slug}/`}
                className="button with-caret--right"
              >
                Next Section
              </Link>
            </div>
          )}
        </div>
      </div>
    );
  }
}

const ChapterList = ({
  sections,
  activeIndex,
  n,
  reportUrl,
  tooltipContent,
  setTooltip
}) => (
  <ul
    style={{
      transform: `translateX(-${activeIndex * 40}px)`,
      position: "relative"
    }}
  >
    <li
      className={n === 0 ? "active" : ""}
      style={{ width: "40px", textAlign: "center", lineHeight: "36px" }}
    >
      <Link
        to={reportUrl}
        className="ga-track-click"
        data-action="click_bottom_nav"
        data-label="report"
        data-value="chapter_skip_home"
      >
        <Home />
      </Link>
    </li>
    {sections.map((s, i) => (
      <li
        className={n === i ? "active" : ""}
        key={`section-${i}`}
        style={{ width: "40px", textAlign: "center" }}
        onMouseEnter={() => {
          setTooltip({
            title: s.title,
            index: i
          });
        }}
        onMouseLeave={() => {
          setTooltip(false);
        }}
      >
        <Link
          to={s.url}
          style={{ display: "block" }}
          className="ga-track-click"
          data-action="click_bottom_nav"
          data-label="report"
          data-value="chapter_skip"
        >
          <h6 className="inline">{i + 1}</h6>
        </Link>
      </li>
    ))}
  </ul>
);

class BottomNav extends Component {
  constructor(props) {
    super(props);
    this.state = {
      tooltipContent: false
    };
  }

  setTooltip = content => {
    this.setState({ tooltipContent: content });
  };

  render() {
    let { section, report, hideAttachments, openMenu } = this.props;
    let next = report.sections[section.number],
      previous = report.sections[section.number - 2];

    let numSections;

    if (report.sections.length < 5) {
      numSections = report.sections.length;
    } else {
      numSections = 5;
    }

    let activeIndex = 0;

    if (section.number < 3) {
      activeIndex = 0;
    } else {
      activeIndex = section.number - 3;
    }

    return (
      <div
        className={`report__bottom-nav-bar row ${
          section.number === report.sections.length ? "last-section" : ""
        }`}
      >
        <div
          className="report__bottom-nav-bar__menu ga-track-click col-3"
          onClick={() => {
            hideAttachments();
            openMenu();
          }}
          data-action="click_bottom_nav"
          data-label="report"
          data-value="open_menu"
        >
          <i className="fa fa-bars" />
          <h6 className="inline">Contents</h6>
        </div>
        <div
          className="report__bottom-nav-bar__chapter-nav col-9"
          style={{ position: "relative", textAlign: "right" }}
        >
          <div className="report__bottom-nav-bar__button-wrapper">
            {section.number > 1 && (
              <Link
                to={report.sections[section.number - 2].url}
                className="prev-button ga-track-click"
                data-action="click_bottom_nav"
                data-label="report"
                data-value="prev_button"
              >
                <h6 className="margin-0">Prev. Section</h6>
              </Link>
            )}
            {section.number === 1 && (
              <Link
                to={report.url}
                className="prev-button"
                data-action="click_bottom_nav"
                data-label="report"
                data-value="prev_button"
              >
                <h6 className="margin-0">Prev. Section</h6>
              </Link>
            )}
          </div>
          <div
            style={{ overflow: "hidden", maxWidth: "240px" }}
            className="report__bottom-nav-bar__chapter-list"
          >
            {this.state.tooltipContent && (
              <Tooltip
                content={this.state.tooltipContent}
                activeIndex={activeIndex}
                numSections={numSections}
              />
            )}
            <ChapterList
              sections={report.sections}
              reportUrl={report.url}
              setTooltip={this.setTooltip}
              tooltipContent={this.state.tooltipContent}
              activeIndex={activeIndex}
              n={section.number - 1}
            />
          </div>
          <div className={`report__bottom-nav-bar__button-wrapper next`}>
            {section.number < report.sections.length && (
              <Link
                to={report.sections[section.number].url}
                className="next-button ga-track-click"
                data-action="click_bottom_nav"
                data-label="report"
                data-value="next_button"
              >
                <h6 className="margin-0">Next Section</h6>
              </Link>
            )}
          </div>
        </div>
      </div>
    );
  }
}

export default BottomNav;
