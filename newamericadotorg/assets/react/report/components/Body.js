import "./Body.scss";

import React, {Component} from "react";
import {render} from "react-dom";
import {connect} from "react-redux";
import ReactDOM from "react-dom";
import Accordion from "../../blocks/accordion";
import Endnote from "./EndnoteAside";
import getProps from "../../../lib/utils/get-props";

class Body extends Component {
    constructor(props) {
        super(props);
        this.state = {
            endnote: null,
            top: 0,
            citeEl: null,
        };
    }

    // repeat of above hack for accordion blocks defined inside Django template.
    addAccordionBlocks = () => {
        let accordionElements = document.querySelectorAll(`.na-react__${Accordion.ID}`);
        if (!accordionElements) return;

        accordionElements.forEach((r) => {
            if (r.hasChildNodes()) return; // already rendered
            let props = getProps(r);
            render(<Accordion.APP {...props} />, r);
        });
    };

    openEndnote = (endnote) => {
        let body = this;

        return function () {
            if (this.querySelector(".report__citation").classList.contains("active")) return body.closeEndnote();
            body.closeEndnote();
            this.querySelector(".report__citation").classList.add("active");
            body.setState({
                endnote,
                top: window.pageYOffset + this.getBoundingClientRect().top - body.el.offsetTop,
                citeEl: this,
            });
        };
    };

    citationEvents = () => {
        let _this = this;
        this.closeEndnote();
        let endnotes = _this.props.report.endnotes;
        let citations = document.querySelectorAll(".report__citation-wrapper");
        this.props.dispatch({
            type: "ADD_SCROLL_EVENT",
            component: "site",
            eventObject: {
                selector: ".report__citation-wrapper",
                onLeave: (el, dir) => {
                    if (this.state.citeEl === el) this.closeEndnote();
                },
                els: citations,
                // viewHeight
                topOffset: -Math.max(document.documentElement.clientHeight, window.innerHeight || 0),
                bottomOffset: -65,
            },
        });
        for (let c of citations) {
            let i = c.getAttribute("data-citation-number") - 1;
            c.onclick = this.openEndnote(endnotes[i]);
        }
    };

    closeEndnote = (el) => {
        if (this.state.citeEl) this.state.citeEl.querySelector(".report__citation").classList.remove("active");
        this.setState({endnote: null, top: -1000, citeEl: null});
    };

    loadScripts = () => {
        let {report, section} = this.props;
        newamericadotorg.renderDataViz();
        if (!this.el) return;
        if (report.data_project_external_script && document.querySelectorAll(".dataviz-project").length) {
            const dataScript = document.createElement("script");

            dataScript.src = `https://na-data-projects.s3.amazonaws.com/projects/${report.data_project_external_script}`;
            dataScript.async = true;

            this.el.appendChild(dataScript);
        }
        let scripts = section.body.match(/<script.*?src="(.*?)"/);
        if (scripts) {
            const script = document.createElement("script");

            script.src = scripts[1];
            script.async = true;

            this.el.appendChild(script);
        }
    };

    componentDidMount() {
        this.citationEvents();
        this.addAccordionBlocks();
        if (this.props.section) this.loadScripts();
    }

    componentDidUpdate(prevProps) {
        this.addAccordionBlocks();
        if (prevProps.section.number != this.props.section.number && this.props.section) {
            // When the section changes, remove the Shorthand embed,
            // allowing it to reinitialize when navigated back to the page.
            if (window.Shorthand) {
                window.Shorthand.remove();
            }
            this.citationEvents();
            this.loadScripts();
            this.props.dispatch({
                type: "RELOAD_SCROLL_EVENTS",
                component: "SITE",
            });
        }
    }

    render() {
        let {section, report} = this.props;
        let {endnotes, date, url, report_pdf, title} = report;
        let {endnote, top} = this.state;
        return (
            <div
                className={`container ${endnote ? "endnote-active" : ""}`}
                ref={(el) => {
                    this.el = el;
                }}
                style={{position: "relative"}}
            >
                <Endnote endnote={endnote} top={top} close={this.closeEndnote} />
                <div className={`report__body${section.hide_title ? " hide-title" : ""}`}>
                    <div className="post-body-wrapper">
                        <h1 className="margin-top-0 report__body__section-title">{section.title}</h1>
                        <div className="report__body__article" dangerouslySetInnerHTML={{__html: section.body}} />
                    </div>
                </div>
            </div>
        );
    }
}

export default Body;
