#ifndef included_PflotranApplicationStrategy
#define included_PflotranApplicationStrategy


#include <string>
#include <vector>

#include "tbox/Array.h"
#include "tbox/Pointer.h"
#include "CellVariable.h"
#include "FaceVariable.h"
#include "PatchHierarchy.h"
#include "VariableContext.h"
#include "FaceData.h"
#include "RefineAlgorithm.h"
#include "RefinePatchStrategy.h"
#include "RefineOperator.h"
#include "CoarsenOperator.h"
#include "SAMRAIVectorReal.h"
#include "tbox/Serializable.h"
#include "CartesianGridGeometry.h"

#include "RefinementBoundaryInterpolation.h"
#include "AMRUtilities.h"
#include "ComponentSelector.h"
#include "ApplicationStrategy.h"
#include "PflotranApplicationParameters.h"
#include "PflotranJacobianMultilevelOperator.h"

namespace SAMRAI{

class PflotranApplicationStrategy: public ApplicationStrategy
{
public:
   PflotranApplicationStrategy(PflotranApplicationParameters *params);
   ~PflotranApplicationStrategy();

   /**
    * Return ComponentSelector of data to allocate on a new level.
    */
   hier::ComponentSelector getDataToAllocate();

   /**
    * Return ComponentSelector of data to time stamp on a new level.
    */
   hier::ComponentSelector getDataToTimeStamp();

   /** 
    * Set initial conditions on new level.
    */
   void setInitialConditions( const double initial_time, tbox::Pointer< hier::PatchLevel<NDIM> > level );

   /**
    * Set initial conditions in specified vector.
    */
   void setInitialConditions( tbox::Pointer< solv::SAMRAIVectorReal<NDIM,double> > ic );

   /** 
    * Set data values on new level.
    */
   void setValuesOnNewLevel( tbox::Pointer< hier::PatchLevel<NDIM> > level );

   /**
    * Return a list of variables used by this application.
    */
   tbox::Array< tbox::Pointer< hier::Variable<NDIM> > > getVariables();

   /**
    * Create the RefineSchedules needed to transfer data to a new level.
    */
   tbox::Array< tbox::Pointer< xfer::RefineSchedule<NDIM> > > setupRegridRefineSchedules( 
      const tbox::Pointer< hier::BasePatchHierarchy<NDIM> > hierarchy, 
      const int level_number,  
      const tbox::Pointer< hier::BasePatchLevel<NDIM> > old_level );

   /**
    * Mark locations where additional refinement is desired.
    */
   void tagCells( const tbox::Pointer< hier::PatchHierarchy<NDIM> > hierarchy,
                          const int level_number,
                          const double error_data_time,
                          const bool initial_time,
                          const int tag_index,
                          const bool uses_richardson_extrapolation_too );

   /**
    * Update data structures that change when the grid hierarchy changes.
    */
   void resetHierarchyConfiguration( const tbox::Pointer< hier::PatchHierarchy<NDIM> > hierarchy,
                                             const int coarsest_level,
                                             const int finest_level );

   /**
    * Evaluate IVP forcing term.
    */
   int evaluateFunction( tbox::Pointer< solv::SAMRAIVectorReal<NDIM,double> >  x,
                         tbox::Pointer< solv::SAMRAIVectorReal<NDIM,double> >  f );

   /**
    * Print identifying std::string.
    */
   void printObjectName( std::ostream& os );

   /**
    * Allocate data for time integrator
    */ 
   void allocateVectorData(SAMRAI::tbox::Pointer<SAMRAI::solv::SAMRAIVectorReal<NDIM,double> > x,
                           double time, bool flag=true ); 


   // Hierarchy
   tbox::Pointer< hier::PatchHierarchy<NDIM> > d_hierarchy;

   void setJacobianMatrix(PflotranJacobianMultilevelOperator *pMatrix){d_Jacobian.reset(pMatrix);}

   void interpolateGlobalToLocalVector(int ndof,
                                       tbox::Pointer< solv::SAMRAIVectorReal<NDIM,double> >  globalVec,
                                       tbox::Pointer< solv::SAMRAIVectorReal<NDIM,double> >  localVec,
                                       int ierr);

   void interpolateLocalToLocalVector(int ndof, 
                                      tbox::Pointer< solv::SAMRAIVectorReal<NDIM,double> >  srcVec,
                                      tbox::Pointer< solv::SAMRAIVectorReal<NDIM,double> >  destVec,
                                      int ierr);

   void setRefinementBoundaryInterpolant(RefinementBoundaryInterpolation *cf_interpolant);

   RefinementBoundaryInterpolation *getRefinementBoundaryInterpolant(void){return d_cf_interpolant; }

protected:

private:

   PflotranApplicationStrategy();

   void initialize(PflotranApplicationParameters *params);
   
   bool d_read_regrid_boxes;
   bool d_is_after_regrid;
   bool d_use_variable_order_interpolation;
   bool d_coarsen_fluxes;
   bool d_error_checkpoint;

   /*
    * We cache a pointer to the grid geometry object to set up initial
    * data and set physical boundary conditions.
    */
   tbox::Pointer<geom::CartesianGridGeometry<NDIM> > d_grid_geometry;

   /*
    * Variables.
    */
   tbox::Pointer< pdat::CellVariable<NDIM,double> > d_solution;

   double d_current_time;

   // Name of application
   std::string d_object_name;

   int d_number_solution_components;

   tbox::Array< tbox::Pointer< hier::Variable<NDIM> > > d_variable_list;

   tbox::Pointer<xfer::RefineOperator<NDIM> >  d_soln_refine_op;
   tbox::Pointer<xfer::CoarsenOperator<NDIM> > d_soln_coarsen_op;

   tbox::Array< tbox::Pointer< xfer::RefineSchedule<NDIM> > > d_regrid_refine_scheds;

   tbox::Array< tbox::Pointer< xfer::RefineSchedule<NDIM> > > d_GlobalToLocalRefineSchedule;

   tbox::Pointer<hier::VariableContext> d_application_ctx;

   hier::ComponentSelector d_AllocSelector;
   hier::ComponentSelector d_TimestampSelector;

   RefinementBoundaryInterpolation *d_cf_interpolant;

   RefinementBoundaryInterpolation::InterpolationScheme d_nl_tangential_interp_scheme;
   RefinementBoundaryInterpolation::InterpolationScheme d_nl_normal_interp_scheme;

   std::auto_ptr<PflotranJacobianMultilevelOperator> d_Jacobian;
};

}

#endif // included_PflotranApplicationStrategy
