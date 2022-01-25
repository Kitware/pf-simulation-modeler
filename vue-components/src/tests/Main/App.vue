<template>
  <v-app>
    <v-app-bar app>
      <div class="text-h6">Parflow Web</div>
      <v-spacer />
      <v-spacer />
      <NavigationDropDown
        :views="mock.NavigationDropDown.views"
        v-model="mock.NavigationDropDown.currentView"
      />
      <v-spacer />
      <v-spacer />
      <v-spacer />
    </v-app-bar>

    <v-main>
      <SimulationType
        v-if="mock.NavigationDropDown.currentView === 'Simulation Type'"
        :shortcuts="mock.SimulationType.shortcuts"
      />
      <OverlayDatabaseErrors
        v-if="mock.NavigationDropDown.currentView === 'Simulation Type'"
        :errors="mock.OverlayDatabaseErrors.errors"
        :workingDirectory="mock.OverlayDatabaseErrors.workingDirectory"
        :fileDB="mock.OverlayDatabaseErrors.fileDB"
      />
      <FileDatabase
        v-if="mock.NavigationDropDown.currentView === 'File Database'"
        :files="mock.FileDatabase.files"
        v-model="mock.FileDatabase.currentFileIndex"
        @updateFiles="updateFiles"
      />
      <Domain v-if="mock.NavigationDropDown.currentView === 'Domain'" />
      <BoundaryConditions
        v-if="mock.NavigationDropDown.currentView === 'Boundary Conditions'"
      />
      <SubSurface
        v-if="mock.NavigationDropDown.currentView === 'Subsurface Properties'"
      />
      <Solver v-if="mock.NavigationDropDown.currentView === 'Solver'" />
      <ProjectGeneration
        v-if="mock.NavigationDropDown.currentView === 'Project Generation'"
        :validation="mock.ProjectGeneration.validation"
      />
    </v-main>
  </v-app>
</template>

<script>
import SimulationType from './components/SimulationType';
import NavigationDropDown from './components/NavigationDropDown';
import OverlayDatabaseErrors from './components/OverlayDatabaseErrors';
import FileDatabase from './components/FileDatabase';
import Domain from './components/Domain';
import BoundaryConditions from './components/BoundaryConditions';
import SubSurface from './components/SubSurface';
import Solver from './components/Solver';
import ProjectGeneration from './components/ProjectGeneration';

import MockData from './MockData';

export default {
  name: 'App',

  components: {
    // Views
    FileDatabase,
    SimulationType,
    Domain,
    BoundaryConditions,
    SubSurface,
    Solver,
    ProjectGeneration,

    // Helpers
    NavigationDropDown,
    OverlayDatabaseErrors,
  },

  data: () => ({
    mock: MockData,
  }),

  methods: {
    updateFiles({ newFile, index }) {
      this.$set(this.mock.FileDatabase.files, index, newFile);
    },
  },
};
</script>
<style>
html {
  overflow: auto;
}
</style>
