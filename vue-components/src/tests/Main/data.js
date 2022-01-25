function daysAgo(days) {
  var now = new Date();
  var oneDayInMilliseconds = 1000 * 60 * 60 * 24 * 2;
  return now - days * oneDayInMilliseconds;
}

export default {
  // Views
  FileDatabase: {
    currentFileIndex: 0,
    files: {
      key1: {
        name: 'MyIndicator',
        description:
          'This is my indicator. I made it. There are many like it, but this one is mine.',
        origin: '/oldDrive/oldFolder/originalProject',
        path: '/opt/fileDatabases/filedb1',
        size: 672716,
        dateModified: daysAgo(100),
        dateUploaded: daysAgo(50),
        type: 'file',
        gridSize: [50, 50, 2],
        category: 'Indicator',
      },
      key2: {
        name: 'Rain Forcing',
        description:
          'This simulates heavy rain across the entire surface. It was made by...',
        origin: '/oldDrive/oldFolder/otherProject',
        path: '/opt/fileDatabases/filedb1',
        size: 5321298,
        dateModified: daysAgo(93),
        dateUploaded: daysAgo(50),
        type: 'zip',
        gridSize: null,
        category: 'CLM',
      },
    },
  },
  SimulationType: {
    shortcuts: {
      wells: false,
      climate: true,
      contaminants: false,
      saturated: 'Variably Saturated',
    },
  },
  // Helpers
  NavigationDropDown: {
    views: [
      'File Database',
      'Simulation Type',
      'Domain',
      'Boundary Conditions',
      'Subsurface Properties',
      //      'Wells',
      //      'CLM',
      'Solver',
      'Project Generation',
    ],
    currentView: 'Simulation Type',
  },
  OverlayDatabaseErrors: {
    errors: [
      /*'Problem 01'*/
    ],
    workingDirectory: '/opt/fake/directory',
    fileDB: '/home/fake/project',
  },
  ProjectGeneration: {
    validation: {
      valid: false,
      output:
        'Parflow run did not validate.\nSolver.TimeStep must be type Int, found 3.14159',
    },
    //validation: {
    //  valid: true,
    //  output: 'Parflow run is validated.',
    //},
  },
};
