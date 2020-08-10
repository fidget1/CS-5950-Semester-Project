import React from 'react';
import {Bar} from 'react-chartjs-2';

export default class TwGraph extends React.Component {
    render() {
        const newData = this.props.data;
        // var data = this.props.data;
        return (
            <div>
                <Bar
                    data={newData}
                    options={{
                        title:{
                            display:true,
                            text:'Average Rainfall per month',
                            fontSize:20
                        },
                        legend:{
                            display:true,
                            position:'right'
                        }
                    }}
                />
            </div>
        );
    }
}