#ifndef PLANAR_SURFACE_HPP
#define PLANAR_SURFACE_HPP

#include <boost/bind.hpp>
#include "Surface.hpp"
#include "Plane.hpp"
//#include "freeFunctions.hpp"

template<typename Ttraits_>
class PlanarSurface
    : public BasicSurfaceImpl<Ttraits_, Plane<typename Ttraits_::world_type::traits_type::length_type> >
{
public:
    typedef BasicSurfaceImpl<Ttraits_, Plane<typename Ttraits_::world_type::traits_type::length_type> > base_type;
    typedef typename base_type::traits_type traits_type;
    typedef typename base_type::identifier_type identifier_type;
    typedef typename base_type::shape_type shape_type;
    typedef typename base_type::rng_type rng_type;
    typedef typename base_type::position_type position_type;
    typedef typename base_type::length_type length_type;

    virtual position_type random_position(rng_type& rng) const
    {
        return ::random_position(base_type::shape(), boost::bind(&rng_type::uniform, rng, -1., 1.));
    }

    virtual position_type random_vector(length_type const& r, rng_type& rng) const
    {
        return multiply(
            normalize(
                add(
                    multiply(
                        base_type::shape().units()[0], rng.uniform(-1., 1.)),
                    multiply(
                        base_type::shape().units()[1], rng.uniform(-1., 1.)))), r);
    }

    virtual position_type bd_displacement(length_type const& r, rng_type& rng) const
    {
        length_type const x(rng.normal(0., r)), y(rng.normal(0., r));
        return add(
            multiply(base_type::shape().unit_x(), x),
            multiply(base_type::shape().unit_y(), y));
    }

    virtual length_type drawR_gbd(Real rnd, length_type r01, Real dt, Real D01, Real v) const
    {
        //TODO: use the 2D BD function instead of the 3D one.
        length_type pair_distance( drawR_gbd_3D(rnd, r01, dt, D01) );
    
        return pair_distance;
    }

    virtual length_type minimal_distance(length_type const& radius) const
    {
        // PlanarSurface has thickness of 0.
        return radius * traits_type::MINIMAL_SEPARATION_FACTOR;
    }

    virtual void accept(ImmutativeStructureVisitor<traits_type> const& visitor) const
    {
        visitor(*this);
    }

    virtual void accept(MutativeStructureVisitor<traits_type> const& visitor)
    {
        visitor(*this);
    }

    PlanarSurface(identifier_type const& id, shape_type const& shape)
        : base_type(id, shape) {}
};


#endif /* PLANAR_SURFACE_HPP */
