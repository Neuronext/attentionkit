import React from "react";
import { Card } from "@shopify/polaris";
import { Line } from "react-chartjs-2";
import electrodeDiagram from "./electrodelocations.png"; 

import { chartStyles, generalOptions } from "../chartOptions";

const specificTranslations = {
  title: "EEG Data Visualization",
  xlabel: "Time",
  ylabel: "Voltage"
};

export function renderModule(channels) {
  const renderCharts = () => {
    const options = {
      ...generalOptions,
      scales: {
        xAxes: [{ scaleLabel: { labelString: specificTranslations.xlabel } }],
        yAxes: [{ scaleLabel: { labelString: specificTranslations.ylabel } }]
      },
      animation: { duration: 0 },
      title: { text: 'Raw data from EEG electrodes' },
      legend: { display: true }
    };

    // Assuming channels.data is already prepared for visualization
    // You might need to adjust this based on how you're managing state and data
    if (channels && channels.data && channels.data.ch0 && channels.data.ch0.datasets[0].data.length > 0) {
      const newData = {
        datasets: channels.data.map((channel, index) => ({
          label: `Channel ${index}`,
          borderColor: `rgba(${217 + index * 40}, ${95 - index * 20}, 2)`,
          data: channel.datasets[0].data,
          fill: false
        })),
        labels: channels.data.ch0.labels // Adjust according to your data structure
      };

      return <Line data={newData} options={options} />;
    } else {
      return <p>Press connect above to see the chart.</p>;
    }
  };

  return (
    <Card title={specificTranslations.title}>
      <Card.Section>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
          <img src={electrodeDiagram} alt="Electrode Locations" style={{ maxWidth: "100%", height: "auto" }} />
          {renderCharts()}
        </div>
      </Card.Section>
    </Card>
  );
}
