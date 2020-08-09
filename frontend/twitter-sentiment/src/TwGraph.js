import React from 'react';
import { transition, axisLeft }  from "d3";
import { scaleLinear } from "d3-scale";
import { max } from 'd3-array';
import { select } from 'd3-selection';

class TwGraph extends React.Component {
    constructor(props) {
        super(props);
        this.createBarChart = this.createBarChart.bind(this);
    }

    // Renders the chart when the component first renders.
    componentDidMount() {
        this.createBarChart();
    }

    // Renders the chart whenever the component 
    // receives new props/state.
    componentDidUpdate() {
        this.createBarChart();
    }

    // Renders the chart
    createBarChart() {
        const node = this.node;
        const svg = select(node)
            .attr("width", this.props.width)
            .attr("height", this.props.height)

        const selection = svg.selectAll("rect").data(this.props.data);
        
        // y axis
        const yScale = scaleLinear()
            .domain([0, max(this.props.data)])
            .range([0, this.props.height])           
        
        svg.append("g").call(axisLeft(yScale));  

        selection
            .transition().duration(300)
            .attr("height", (d) => yScale(d))
            .attr("y", (d) => this.props.height - yScale(d))

        selection
            .enter()
            .append("rect")
            .attr("x", (d, i) => i * 45)
            .attr("y", (d) => this.props.height)
            .attr("width", 40)
            .attr("height", 0)
            .attr("fill", "#5dbced")
            .transition().duration(300)
            .attr("height", (d) => yScale(d))
            .attr("y", (d) => this.props.height - yScale(d))

        selection
            .exit()
            .transition().duration(300)
            .attr("y", (d) => this.props.height)
            .attr("height", 0)
            .remove()
    }

    render() {
        return (
            <section id="tw-graph">
                <svg ref={node => this.node = node}>
                </svg>
            </section>           
        );
    }
}

export default TwGraph;