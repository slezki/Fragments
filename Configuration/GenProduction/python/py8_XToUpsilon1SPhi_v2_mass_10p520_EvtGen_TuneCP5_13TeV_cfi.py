# cfg file for X -> Ups(1S) K+ K-. Masses and widths are 0.
#The mass of the X is set to 10.5 GeV (desired resonant mass)

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13000.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            list_forced_decays = cms.vstring('myX'),       
            operates_on_particles = cms.vint32(10551),        
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
            """
            Particle Upsilon 9.4603000 0.00005402
            Particle phi 1.019461 0.004249
            Particle chi_b0  10.520000 0.00000

            Alias myUpsilon Upsilon
            Alias myPhi     phi
            Alias myX    chi_b0 

            Decay myUpsilon
            1.0   mu+  mu-         PHOTOS  VLL;
            Enddecay

            Decay myPhi
            1.0   K+  K-           VSS;
            Enddecay

            Decay myX
            1.0   myUpsilon myPhi  PHSP;
            Enddecay

            End
            """
            )
	),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
	pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'Bottomonium:states(3PJ) = 10551',   
            'Bottomonium:O(3PJ)[3P0(1)] = 0.085',
            'Bottomonium:O(3PJ)[3S1(8)] = 0.04',
            'Bottomonium:gg2bbbar(3PJ)[3PJ(1)]g = on',
            'Bottomonium:qg2bbbar(3PJ)[3PJ(1)]q = on',
            'Bottomonium:qqbar2bbbar(3PJ)[3PJ(1)]g = on',
            'Bottomonium:gg2bbbar(3PJ)[3S1(8)]g = on',
            'Bottomonium:qg2bbbar(3PJ)[3S1(8)]q = on',
            'Bottomonium:qqbar2bbbar(3PJ)[3S1(8)]g = on',
            'PhaseSpace:pTHatMin = 10.', #minimum transverse momenta in the rest frame of the process
            '10551:m0 = 10.52',  
            '10551:mWidth = 0.0',      
            '10551:onMode = off',
            '10551:onIfMatch = 553 333',
            '553:onMode = off',
            '553:onIfMatch = 13 -13',
            '333:onMode = off',
            '333:onIfMatch = 321 -321'
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters'
                                    )
    )
)

pwaveIDfilter = cms.EDFilter("MCSingleParticleFilter",
    ParticleID = cms.untracked.vint32(10551),
    MinPt = cms.untracked.vdouble(15.0),
    MinEta = cms.untracked.vdouble(-9999.0),
    MaxEta = cms.untracked.vdouble(9999.0),
    Status = cms.untracked.vint32(2)
)

decayfilter = cms.EDFilter("PythiaDauVFilter",
    ParticleID = cms.untracked.int32(10551),
    NumberDaughters = cms.untracked.int32(2),
    DaughterIDs = cms.untracked.vint32(553, 333),
    MaxEta = cms.untracked.vdouble(9999.0, 9999.0),
    MinEta = cms.untracked.vdouble(-9999.0, -9999.0),
    MinPt = cms.untracked.vdouble(5.0, 0.5),
)

upsfilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(10551),
    ParticleID = cms.untracked.int32(553),
    NumberDaughters = cms.untracked.int32(2),
    DaughterIDs = cms.untracked.vint32(13, -13),
    MinPt = cms.untracked.vdouble(1.5, 1.5),
    MaxEta = cms.untracked.vdouble(2.5, 2.5),
    MinEta = cms.untracked.vdouble(-2.5, -2.5),
)

phifilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(10551),
    ParticleID = cms.untracked.int32(333),
    NumberDaughters = cms.untracked.int32(2),
    DaughterIDs = cms.untracked.vint32(321, -321),
    MinPt = cms.untracked.vdouble(0.5, 0.5),
    MaxEta = cms.untracked.vdouble(2.5, 2.5),
    MinEta = cms.untracked.vdouble(-2.5, -2.5),
)

ProductionFilterSequence = cms.Sequence(generator*pwaveIDfilter*decayfilter*upsfilter*phifilter)