#ifndef STRUCTURE_HPP
#define STRUCTURE_HPP

#include <ostream>
#if defined(HAVE_TR1_FUNCTIONAL)
#include <tr1/functional>
#elif defined(HAVE_STD_HASH)
#include <functional>
#elif defined(HAVE_BOOST_FUNCTIONAL_HASH_HPP)
#include <boost/functional/hash.hpp>
#endif

#include <sstream>
#include "Vector3.hpp"
#include "freeFunctions.hpp"

template<typename Ttraits_>
class Structure
{
public:
    typedef Ttraits_ traits_type;
    typedef typename traits_type::rng_type rng_type;
    typedef typename traits_type::structure_id_type identifier_type;
    typedef typename traits_type::length_type length_type;
    typedef typename traits_type::position_type position_type;
    typedef std::pair<position_type, length_type> projected_type;

public:
    virtual ~Structure() {}

    identifier_type const& id() const
    {
        return id_;
    }

    virtual bool operator==(Structure const& rhs) const
    {
        return id_ == rhs.id();
    }

    bool operator!=(Structure const& rhs) const
    {
        return !operator==(rhs);
    }

    virtual position_type random_position(rng_type& rng) const = 0;

    virtual position_type random_vector(length_type const& r, rng_type& rng) const = 0;

    virtual position_type bd_displacement(length_type const& mean, length_type const& r, rng_type& rng) const = 0;

    virtual length_type drawR_gbd(Real const& rnd, length_type const& r01, Real const& dt, Real const& D01, Real const& v) const = 0;

    virtual Real p_acceptance(Real const& k_a, Real const& dt, length_type const& r01, position_type const& ipv, Real const& D0, Real const& D1, Real const& v0, Real const& v1) const = 0;

    virtual position_type dissociation_vector(rng_type& rng, length_type const& r01, Real const& dt, Real const& D01, Real const& v) const = 0;

    virtual Real reaction_volume( length_type const& r0, length_type const& r1, length_type const& rl ) const = 0;

    virtual position_type newbd_dissociation_vector( rng_type& rng, length_type const& r01, length_type const& rl ) const = 0;

    virtual projected_type projected_point(position_type const& pos) const = 0;

    virtual std::size_t hash() const
    {
#if defined(HAVE_TR1_FUNCTIONAL)
        using std::tr1::hash;
#elif defined(HAVE_STD_HASH)
        using std::hash;
#elif defined(HAVE_BOOST_FUNCTIONAL_HASH_HPP)
        using boost::hash;
#endif
        return hash<identifier_type>()(id_);
    }

    virtual std::string as_string() const
    {
        std::ostringstream out;
        out << "Structure(" << id() << ")";
        return out.str();
    }

    Structure(identifier_type const& id)
        : id_(id) {}

protected:
    identifier_type id_;
};

template<typename Tstrm, typename Ttraits, typename T_traits>
inline std::basic_ostream<Tstrm, Ttraits>& operator<<(std::basic_ostream<Tstrm, Ttraits>& strm, const Structure<T_traits>& v)
{
    strm << v.as_string(); 
    return strm;
}

#if defined(HAVE_TR1_FUNCTIONAL)
namespace std { namespace tr1 {
#elif defined(HAVE_STD_HASH)
namespace std {
#elif defined(HAVE_BOOST_FUNCTIONAL_HASH_HPP)
namespace boost {
#endif

template<typename Ttraits>
struct hash<Structure<Ttraits> >
{
    typedef Structure<Ttraits> argument_type;

    std::size_t operator()(argument_type const& val)
    {
        return val.hash();
    }
};

#if defined(HAVE_TR1_FUNCTIONAL)
} } // namespace std::tr1
#elif defined(HAVE_STD_HASH)
} // namespace std
#elif defined(HAVE_BOOST_FUNCTIONAL_HASH_HPP)
} // namespace boost
#endif

#endif /* STRUCTURE_HPP */
