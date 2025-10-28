import React from 'react';

const ReportOutput = ({ note, warnings, confidence }) => {
  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
      <h2 className="text-xl font-bold text-gray-800 mb-4">Generated Clinical Note</h2>
      <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4 max-h-96 overflow-y-auto">
        {note ? (
          <pre className="whitespace-pre-wrap text-sm text-gray-700 font-sans">{note}</pre>
        ) : (
          <p className="text-gray-500 italic">Clinical note will appear here...</p>
        )}
      </div>

      <div className="flex flex-wrap justify-between items-center gap-2">
        <div className="text-sm">
          <span className="font-medium text-gray-700">Confidence:</span>{' '}
          <span className="font-bold">{confidence ? `${(confidence * 100).toFixed(1)}%` : 'N/A'}</span>
        </div>
        {warnings && warnings.length > 0 && (
          <div className="text-sm">
            <span className="font-medium text-red-700">Warnings:</span>{' '}
            <span className="text-red-600">{warnings.join(', ')}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default ReportOutput;